import Shared.constants.NetConstants as NetConstants;
import Shared.constants.LogConstants as LogConstants;
from Shared.dtos.PlayerGameIdentifierDto import PlayerGameIdentifierDto;
from Shared.dtos.UpdatedEntityDto import UpdatedEntityDto;
from Shared.dtos.ConnectDto import ConnectDto;
from Shared.dtos.GameActionDto import GameActionDto;
from Shared.dtos.CreateGameDto import CreateGameDto;
from Shared.dtos.AddAgentGameDto import AddAgentGameDto;
from Shared.Packet import Packet;

import Client.utility.PacketUtility as PacketUtility;
import socket;
import pickle;
import uuid;

class ServiceContext():
    def __init__(self, context):
        self.__context = context;
        self.__connection = None;
        self.__lastUpdatedUtc = None;

    @property
    def ViewModelContext(self):
        return self.__context;

    @property
    def Client(self):
        if not self.__context:
            return None;

        return self.__context.Client;

    # General Connection

    def Send(self, data):
        try:
            # We send some data
            self.__connection.sendall(pickle.dumps(data));

            # We get some reply
            serializedReply = self.__connection.recv(4 * NetConstants.KILOBYTE);

            # this is some serialized object
            reply = pickle.loads(serializedReply);

            return reply;

            print(reply);
        except socket.error as error:
            print(LogConstants.ERROR + " " + str(error));

        return;

    def Connect(self):
        try:
            self.__connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
            self.__connection.connect(NetConstants.ADDRESS);

            dto = ConnectDto(self.Client.Name, self.Client.Identifier);
            packet = PacketUtility.GetConnectPacket(dto);

            reply = self.Send(packet);

            self.Client.SetPlayer(reply);

            return reply;
        except Exception as error:
            print(LogConstants.ERROR + " " + str(error));

        return;

    def Disconnect(self):
        if not self.__connection:
            return;

        try:
            self.LeaveGame();
            self.__connection.close();
        except Exception as error:
            print(LogConstants.ERROR + " " + str(error));
            return;

        return;

    #endregion

    #region Game Calls

    def GetGamesList(self):
        packet = PacketUtility.GetGamesPacket();

        reply = self.Send(packet);

        return reply;

    def LeaveGame(self):
        if not self.Client.GameIdentifier:
            return;

        dto = PlayerGameIdentifierDto(self.Client.Player, self.Client.GameIdentifier);
        packet = PacketUtility.GetLeaveGamePacket(dto)

        reply = self.Send(packet);

        if reply:
            self.Client.SetGame(None);

        return reply;

    def CreateGame(self, gameName):

        dto = CreateGameDto(self.Client.Player, gameName)
        packet = PacketUtility.GetCreateGamePacket(dto);

        reply = self.Send(packet);

        if not reply:
            return None;

        self.Client.SetGame(reply.Entity);
        self.__lastUpdatedUtc = reply.UpdatedUtc;

        return reply;

    def JoinGame(self, gameIdentifier):
        dto = PlayerGameIdentifierDto(self.Client.Player, gameIdentifier)
        packet = PacketUtility.GetJoinGamePacket(dto);

        reply = self.Send(packet);

        self.Client.SetGame(reply.Entity);
        self.__lastUpdatedUtc = reply.UpdatedUtc;

        return reply;

    def GetGameLobby(self):
        if not self.Client.GameIdentifier:
            return None;

        dto = PlayerGameIdentifierDto(self.Client.Player, self.Client.GameIdentifier);
        wrapperDto = UpdatedEntityDto(dto, self.__lastUpdatedUtc);

        packet = PacketUtility.GetGameLobbyPacket(wrapperDto);

        reply = self.Send(packet);

        self.Client.SetGame(reply.Entity.Game);
        self.Client.SetPlayer(reply.Entity.Player);
        self.__lastUpdatedUtc = reply.UpdatedUtc;

        return self.Client.Game;

    def AddAgentToGame(self, agentType):
        if not self.Client.GameIdentifier or not agentType:
            return None;

        dto = AddAgentGameDto(self.Client.Player, self.Client.GameIdentifier, agentType);
        packet = PacketUtility.GetAddAgentToGamePacket(dto);

        reply = self.Send(packet);
        return reply;

    def RemoveAgentFromGame(self):
        if not self.Client.GameIdentifier:
            return None;

        dto = PlayerGameIdentifierDto(self.Client.Player, self.Client.GameIdentifier);
        packet = PacketUtility.GetRemoveAgentFromGamePacket(dto);

        reply = self.Send(packet);
        return reply;

    def VoteStart(self):
        if not self.Client.GameIdentifier:
            return None;

        dto = PlayerGameIdentifierDto(self.Client.Player, self.Client.GameIdentifier);
        wrapperDto = UpdatedEntityDto(dto, self.__lastUpdatedUtc);

        packet = PacketUtility.GetVoteGameStartPacket(wrapperDto);

        reply = self.Send(packet);

        return reply;

    # Villager / Common
    def Talk(self, message):
        if not message or not message.IsValid:
            return;

        packet = PacketUtility.GetTalkPacket(message);

        reply = self.Send(packet);

        return reply;

    def Vote(self, targetPlayerIdentifier):
        if not self.Client or\
            not self.Client.GameIdentifier or\
            not self.Client.Player or\
            not targetPlayerIdentifier:
            # null check both the current player and the target player
            return;

        dto = GameActionDto(self.Client.GameIdentifier, self.Client.Player, targetPlayerIdentifier);
        packet = PacketUtility.GetVotePlayerPacket(dto);

        reply = self.Send(packet);

        return reply;

    def Wait(self):
        if not self.Client or\
            not self.Client.GameIdentifier or\
            not self.Client.Player:

            return;

        dto = GameActionDto(self.Client.GameIdentifier, self.Client.Player, None);
        packet = PacketUtility.GetVotePlayerPacket(dto);

        reply = self.Send(packet);

        return reply;

    # Werewolf
    def Whisper(self, message):
        if not message or not message.IsValid:
            return;

        packet = PacketUtility.GetWhisperPacket(message);

        reply = self.Send(packet);

        return reply;

    def Attack(self, targetPlayerIdentifier):
        if not self.Client or\
            not self.Client.GameIdentifier or\
            not self.Client.Player or\
            not targetPlayerIdentifier:
            # null check both the current player and the target player
            return;

        dto = GameActionDto(self.Client.GameIdentifier, self.Client.Player, targetPlayerIdentifier);
        packet = PacketUtility.GetAttackPlayerPacket(dto);

        reply = self.Send(packet);

        return reply;

    # Seer
    def Divine(self, targetPlayerIdentifier):
        if not self.Client or\
            not self.Client.GameIdentifier or\
            not self.Client.Player or\
            not targetPlayerIdentifier:
            # null check both the current player and the target player
            return;

        dto = GameActionDto(self.Client.GameIdentifier, self.Client.Player, targetPlayerIdentifier);
        packet = PacketUtility.GetDivinePlayerPacket(dto);

        reply = self.Send(packet);

        return reply;

    # Guard
    def Guard(self, targetPlayerIdentifier):
        if not self.Client or\
            not self.Client.GameIdentifier or\
            not self.Client.Player or\
            not targetPlayerIdentifier:
            # null check both the current player and the target player
            return;

        dto = GameActionDto(self.Client.GameIdentifier, self.Client.Player, targetPlayerIdentifier);
        packet = PacketUtility.GetGuardPlayerPacket(dto);

        reply = self.Send(packet);

        return reply;

    #endregion
