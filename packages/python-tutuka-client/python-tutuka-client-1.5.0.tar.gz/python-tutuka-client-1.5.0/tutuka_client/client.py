from datetime import datetime
from typing import Optional

from tutuka_client.base import BaseClient
from tutuka_client.errors import TutukaException
from tutuka_client.stop_reasons import CARD_STOP_REASONS
from tutuka_client.utils import date_time_normalize


class LocalApiClient(BaseClient):
    def create_linked_card(
        self,
        reference_id: str,
        first_name: str,
        last_name: str,
        id_or_passport: str,
        expiry_date: datetime,
        transaction_id: str,
        cell_phone_number: Optional[str] = '',
    ):
        return self.execute(
            method_name='CreateLinkedCard',
            arguments=[
                self.terminal_id,
                reference_id,
                first_name,
                last_name,
                id_or_passport,
                cell_phone_number,
                expiry_date,
                transaction_id,
            ],
        )

    def link_card(
        self,
        reference_id: str,
        card_identifier: str,
        first_name: str,
        last_name: str,
        id_or_passport: str,
        transaction_id: str,
        cell_phone_number: Optional[str] = '',
    ):
        return self.execute(
            method_name='LinkCard',
            arguments=[
                self.terminal_id,
                reference_id,
                card_identifier,
                first_name,
                last_name,
                id_or_passport,
                cell_phone_number,
                transaction_id,
            ],
        )

    def order_card(
        self,
        title: str,
        last_name: str,
        transaction_id: str,
        initials: Optional[str] = '',
        address1: Optional[str] = '',
        address2: Optional[str] = '',
        address3: Optional[str] = '',
        address4: Optional[str] = '',
        address5: Optional[str] = '',
        additional_data: Optional[str] = '',
    ):
        return self.execute(
            method_name='OrderCard',
            arguments=[
                self.terminal_id,
                title,
                initials,
                last_name,
                address1,
                address2,
                address3,
                address4,
                address5,
                additional_data,
                transaction_id,
            ],
        )

    def order_card_with_pin_block(  # noqa: WPS211
        self,
        title: str,
        last_name: str,
        pin_block: str,
        transaction_id: str,
        initials: Optional[str] = '',
        address1: Optional[str] = '',
        address2: Optional[str] = '',
        address3: Optional[str] = '',
        address4: Optional[str] = '',
        address5: Optional[str] = '',
        additional_data: Optional[str] = '',
    ):
        return self.execute(
            method_name='OrderCardWithPinBlock',
            arguments=[
                self.terminal_id,
                title,
                initials,
                last_name,
                address1,
                address2,
                address3,
                address4,
                address5,
                additional_data,
                pin_block,
                transaction_id,
            ],
        )

    def activate_card(self, card_identifier: str, transaction_id: str):
        return self.execute(
            method_name='ActivateCard',
            arguments=[
                self.terminal_id,
                card_identifier,
                transaction_id,
            ],
        )

    def get_active_linked_cards(self, reference_id: str, transaction_id: str):
        active_linked_cards = self.execute(
            method_name='GetActiveLinkedCards',
            arguments=[
                self.terminal_id,
                reference_id,
                transaction_id,
            ],
        )
        active_linked_cards['cards'] = [
            {
                key: date_time_normalize(value)
                for (key, value) in card.items()  # noqa: WPS110
            } for card in active_linked_cards['cards']
        ]
        return active_linked_cards

    def get_linked_cards(self, reference_id: str, transaction_id: str):
        linked_cards = self.execute(
            method_name='GetLinkedCards',
            arguments=[
                self.terminal_id,
                reference_id,
                transaction_id,
            ],
        )
        linked_cards['cards'] = [
            {
                key: date_time_normalize(value)
                for (key, value) in card.items()  # noqa: WPS110
            } for card in linked_cards['cards']
        ]
        return linked_cards

    def change_pin(
        self,
        reference_id: str,
        card_identifier: str,
        new_pin: str,
        transaction_id: str,
    ):
        return self.execute(
            method_name='ChangePin',
            arguments=[
                self.terminal_id,
                reference_id,
                card_identifier,
                new_pin,
                transaction_id,
            ],
        )

    def reset_pin(self, reference_id: str, card_identifier: str, transaction_id: str):
        return self.execute(
            method_name='ResetPin',
            arguments=[
                self.terminal_id,
                reference_id,
                card_identifier,
                transaction_id,
            ],
        )

    def update_bearer(
        self,
        reference_id: str,
        card_identifier: str,
        first_name: str,
        last_name: str,
        id_or_passport: str,
        cell_phone_number: str,
        transaction_id: str,
    ):
        return self.execute(
            method_name='UpdateBearer',
            arguments=[
                self.terminal_id,
                reference_id,
                card_identifier,
                first_name,
                last_name,
                id_or_passport,
                cell_phone_number,
                transaction_id,
            ],
        )

    def transfer_link(
        self,
        reference_id: str,
        old_card_identifier: str,
        new_card_identifier: str,
        transaction_id: str,
    ):
        return self.execute(
            method_name='TransferLink',
            arguments=[
                self.terminal_id,
                reference_id,
                old_card_identifier,
                new_card_identifier,
                transaction_id,
            ],
        )

    def stop_card(
        self,
        reference_id: str,
        card_identifier: str,
        reason: str,
        note: str,
        transaction_id: str,
    ):
        if reason not in CARD_STOP_REASONS:
            raise TutukaException(
                'invalid card stop reason: {reason}'.format(reason=reason),
            )

        return self.execute(
            method_name='StopCard',
            arguments=[
                self.terminal_id,
                reference_id,
                card_identifier,
                CARD_STOP_REASONS[reason],
                note,
                transaction_id,
            ],
        )

    def unstop_card(
        self,
        reference_id: str,
        card_identifier: str,
        note: str,
        transaction_id: str,
    ):
        return self.execute(
            method_name='UnstopCard',
            arguments=[
                self.terminal_id,
                reference_id,
                card_identifier,
                note,
                transaction_id,
            ],
        )

    def status(self, reference_id: str, card_identifier: str, transaction_id: str):
        return self.execute(
            method_name='Status',
            arguments=[
                self.terminal_id,
                reference_id,
                card_identifier,
                transaction_id,
            ],
        )

    def set3d_secure_code(
        self,
        reference_id: str,
        card_identifier: str,
        code: str,
        transaction_id: str,
    ):
        return self.execute(
            method_name='Set3dSecureCode',
            arguments=[
                self.terminal_id,
                reference_id,
                card_identifier,
                code,
                transaction_id,
            ],
        )

    def update_cvv(
        self,
        reference_id: str,
        card_identifier: str,
        transaction_id: str,
    ):
        return self.execute(
            method_name='UpdateCVV',
            arguments=[
                self.terminal_id,
                reference_id,
                card_identifier,
                transaction_id,
            ],
        )

    def retire_card(
        self,
        reference_id: str,
        card_identifier: str,
        transaction_id: str,
    ):
        return self.execute(
            method_name='RetireCard',
            arguments=[
                self.terminal_id,
                reference_id,
                card_identifier,
                transaction_id,
            ],
        )

    def administrative_message(
        self,
        reference_id: str,
        message_name: str,
        transaction_id: str,
        message_data: Optional[str] = '',
    ):
        return self.execute(
            method_name='AdministrativeMessage',
            arguments=[
                self.terminal_id,
                reference_id,
                message_name,
                message_data,
                transaction_id,
            ],
        )

    def activate_token(
        self,
        reference: str,
        card_identifier: str,
        reason_code: str,
        transaction_id: str,
        comment: Optional[str] = '',
        token_unique_reference: Optional[str] = '',
        activation_code: Optional[str] = '',
    ):
        return self.execute(
            method_name='ActivateToken',
            arguments=[
                self.terminal_id,
                reference,
                card_identifier,
                token_unique_reference,
                activation_code,
                reason_code,
                comment,
                transaction_id,
            ],
        )

    def delete_token(
        self,
        reference: str,
        card_identifier: str,
        stop_reason_id: int,
        transaction_id: str,
        comment: Optional[str] = '',
        token_unique_reference: Optional[str] = '',
    ):
        return self.execute(
            method_name='DeleteToken',
            arguments=[
                self.terminal_id,
                reference,
                card_identifier,
                token_unique_reference,
                stop_reason_id,
                comment,
                transaction_id,
            ],
        )

    def list_tokens(
        self,
        reference: str,
        card_identifier: str,
        transaction_id: str,
    ):
        return self.execute(
            method_name='ListTokens',
            arguments=[
                self.terminal_id,
                reference,
                card_identifier,
                transaction_id,
            ],
        )

    def stop_token(
        self,
        reference: str,
        card_identifier: str,
        stop_reason_id: int,
        transaction_id: str,
        comment: Optional[str] = '',
        token_unique_reference: Optional[str] = '',
    ):
        return self.execute(
            method_name='StopToken',
            arguments=[
                self.terminal_id,
                reference,
                card_identifier,
                token_unique_reference,
                stop_reason_id,
                comment,
                transaction_id,
            ],
        )

    def transfer_token(
        self,
        reference: str,
        token_unique_reference: str,
        old_card_identifier: str,
        new_card_identifier: str,
        transaction_id: str,
    ):
        return self.execute(
            method_name='TransferToken',
            arguments=[
                self.terminal_id,
                reference,
                token_unique_reference,
                old_card_identifier,
                new_card_identifier,
                transaction_id,
            ],
        )

    def unstop_token(
        self,
        reference: str,
        card_identifier: str,
        unstop_reason_id: int,
        transaction_id: str,
        comment: Optional[str] = '',
        token_unique_reference: Optional[str] = '',
    ):
        return self.execute(
            method_name='UnstopToken',
            arguments=[
                self.terminal_id,
                reference,
                card_identifier,
                token_unique_reference,
                unstop_reason_id,
                comment,
                transaction_id,
            ],
        )
