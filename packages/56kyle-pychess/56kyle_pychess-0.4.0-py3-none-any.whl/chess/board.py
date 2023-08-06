from dataclasses import replace, dataclass
from typing import Set, Dict, Type, Iterable

from chess.bishop import Bishop
from chess.castle_right import CastleRight
from chess.color import Color
from chess.king import KingType
from chess.knight import Knight
from chess.line import Line
from chess.move import Move
from chess.offset import Offset
from chess.pawn import PawnType

from chess.piece import Piece
from chess.position import Position
from chess.position_constants import *
from chess.queen import Queen
from chess.rect import Rect
from chess.rook import Rook, RookType
from chess.segment import Segment


class Board:
    rect: Rect = Rect(p1=A1, p2=H8)
    color_promotion_positions: Dict[Color, Set[Position]] = {
        Color.WHITE: {Position(file=file, rank=8) for file in range(1, 9)},
        Color.BLACK: {Position(file=file, rank=1) for file in range(1, 9)},
    }
    allowed_promotions: Set[Type[Piece]] = {
        Knight,
        Bishop,
        Rook,
        Queen,
    }

    def __init__(self,
                 pieces: Set[Piece],
                 castling_rights: Set[CastleRight] = None,
                 en_passant_target_position: Position = None,
                 half_move_draw_clock: int = 0,
                 full_move_number: int = 0):
        self.pieces: Set[Piece] = pieces if pieces else set()
        self.castling_rights: Set[CastleRight] = castling_rights if castling_rights else set()
        self.en_passant_target_position: Position = en_passant_target_position
        self.half_move_draw_clock: int = half_move_draw_clock
        self.full_move_number: int = full_move_number

    def move(self, piece: Piece, destination: Position):
        self._validate_destination_is_empty(destination=destination)
        self._validate_in_bounds(position=destination)

        self.pieces.remove(piece)
        self.pieces.add(piece.move(destination))

    def _validate_destination_is_empty(self, destination: Position):
        if self.get_piece(destination) is not None:
            raise ValueError(f'Piece already at {destination}')

    def _validate_in_bounds(self, position: Position):
        if position not in self.rect:
            raise ValueError(f'Position {position} is out of bounds')

    def promote(self, piece: Piece, promotion: Type[Piece]):
        self._validate_is_allowed_promotion(promotion=promotion)
        self.pieces.remove(piece)
        self.pieces.add(piece.promote(promotion=promotion))

    def _validate_is_allowed_promotion(self, promotion: Type[Piece]):
        if promotion not in self.allowed_promotions:
            raise ValueError(f'Invalid promotion: {promotion}')

    def get_colored_pieces(self, color: Color) -> Set[Piece]:
        return {piece for piece in self.pieces if piece.color == color}

    def get_piece(self, position: Position) -> Piece | None:
        for piece in self.pieces:
            if piece.position == position:
                return piece
        return None

    def is_promotion_position(self, color: Color, position: Position) -> bool:
        return position in self.color_promotion_positions[color]

    def is_check_present(self, color: Color = None) -> bool:
        for piece in self.pieces:
            targets = self.get_piece_capture_targets(piece=piece)
            for targeted_piece in targets:
                if targeted_piece.color == color or color is None:
                    if targeted_piece.type == KingType:
                        return True
        return False

    def get_first_encountered_piece_in_line(self, line: Line) -> Piece | None:
        closest_piece: Piece | None = None
        closest_distance: float | None = None
        for piece in self.pieces:
            if piece.position in line and piece.position != line.p1:
                distance = piece.position.distance_to(line.p1)
                if closest_distance is None or distance < closest_distance:
                    closest_piece = piece
                    closest_distance = distance
        return closest_piece

    def get_piece_moves(self, piece: Piece) -> Set[Move]:
        movement_moves: Set[Move] = self.get_piece_movement_moves(piece=piece)
        capture_moves: Set[Move] = self.get_piece_capture_moves(piece=piece)
        en_passant_moves: Set[Move] = self.get_piece_en_passant_moves(piece=piece)
        castle_moves: Set[Move] = self.get_piece_castle_moves(piece=piece)
        return movement_moves | capture_moves

    def get_piece_movement_moves(self, piece: Piece) -> Set[Move]:
        movements = self.get_piece_movements(piece=piece)
        return {
            Move(piece=piece, origin=piece.position, destination=position, captures=set()) for position in movements
        }

    def get_piece_movements(self, piece: Piece) -> Set[Position]:
        movements = set()

        for line in piece.get_move_lines():
            for position in self._iter_line_positions(line):
                if self.get_piece(position) is not None:
                    break
                movements.add(position)
        return movements

    def _iter_line_positions(self, line: Line) -> Iterable[Position]:
        dx = line.p2.file - line.p1.file
        dy = line.p2.rank - line.p1.rank
        current_position: Position = line.p2
        while current_position in self.rect and current_position in line:
            yield current_position
            current_position = current_position.offset(dx=dx, dy=dy)

    def get_piece_capture_moves(self, piece: Piece) -> Set[Move]:
        targets = self.get_piece_capture_targets(piece=piece)
        return {
            Move(piece=piece, origin=piece.position, destination=target.position, captures={target}) for target in targets
        }

    def get_piece_capture_targets(self, piece: Piece) -> Set[Piece]:
        targets = set()
        for line in piece.get_capture_lines():
            encountered_piece: Piece | None = self.get_first_encountered_piece_in_line(line)
            if encountered_piece is not None and piece.is_enemy(piece=encountered_piece):
                targets.add(encountered_piece)
        return targets

    def get_piece_en_passant_moves(self, piece: Piece) -> Set[Move]:
        targets = self.get_piece_en_passant_targets(piece=piece)
        return {
            Move(piece=piece, origin=piece.position, destination=target.position, captures={target}) for target in targets
        }

    def get_piece_en_passant_targets(self, piece: Piece) -> Set[Piece]:
        targets = set()
        if self.en_passant_target_position is not None:
            for line in piece.get_en_passant_lines():
                if self.en_passant_target_position in line:
                    encountered_piece: Piece | None = self.get_piece(
                            replace(self.en_passant_target_position, rank=piece.position.rank)
                        )
                    if encountered_piece is not None and piece.is_enemy(piece=encountered_piece):
                        targets.add(encountered_piece)
        return targets

    def get_piece_threat_map(self, piece: Piece) -> Set[Position]:
        threat_map = set()
        for line in piece.get_capture_lines():
            for position in self._iter_line_positions(line):
                threat_map.add(position)
                if self.get_piece(position) is not None:
                    break
        return threat_map

    def get_piece_castle_moves(self, piece: Piece) -> Set[Move]:
        for castle_right in self.castling_rights:
            if piece.type != KingType:
                continue
            if piece.color != castle_right.color:
                continue
            if piece.position != castle_right.king_origin:
                continue

            rook_origin_contents: Piece | None = self.get_piece(castle_right.rook_origin)
            if rook_origin_contents is None:
                continue
            if rook_origin_contents.type != RookType:
                continue
            if rook_origin_contents.color != castle_right.color:
                continue
            if rook_origin_contents.has_moved:
                continue

            if not self.is_castle_path_clear(castle_right=castle_right):
                continue

    def is_castle_path_clear(self, castle_right: CastleRight) -> bool:
        king_path: Segment = Segment(p1=castle_right.king_origin, p2=castle_right.king_destination)
        possible_enemy_movements: Set[Position] = set()

