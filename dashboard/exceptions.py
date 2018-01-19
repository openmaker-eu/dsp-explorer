class EmailAlreadyUsed(Exception):
    message = "Email already Used"

class UserAlreadyInvited(Exception):
    message = "User already invited"


class InvitationAlreadyExist(Exception):
    message = "Invitation already send this user"


class SelfInvitation(Exception):
    message = "You can not invite yourself"

class InvitationDoesNotExist(Exception):
    message = "Invitation does not exist"
