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


def is_only_invited_user(user: User, paper: Paper) -> bool:
	"""
		초대된 유저인지를 확인함.
		호스트인지 말고 초대된 유저인지만 판단해야할 때도 있어서 추가함
	"""
	return paper.invitingUser.filter(pk=user.id).exists()