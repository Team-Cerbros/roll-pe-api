from paper.models import Paper
from user.models import User



def is_host(user: User, paper: Paper) -> bool:
	"""
		Host인지 확인함.
	"""
	return True if paper.hostFK == user else False


def is_invited_user(user: User, paper: Paper) -> bool:
	"""
		Host이거나 초대된 유저인지를 확인함.
	"""
	if is_host(user, paper):
		return True
	else:
		if user in paper.invitingUser:
			return True
		else:
			return False