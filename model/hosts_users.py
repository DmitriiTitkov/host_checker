from model import AbstractDBModule


class HostsUsers(AbstractDBModule):
    async def add_user_host(self, host_id: int, user_id: int):
        super()
        pass


    async def remove_user_host(self, host_id: int, user_id: int):
        pass