import vk_api
from datetime import datetime

access_token = "9609a7a29609a7a29609a7a2cd9679b5c4996099609a7a2c8576730427857bd9e2dcdd0"


class VkService:
    vk_session = vk_api.VkApi(token=access_token)
    vk = vk_session.get_api()

    @staticmethod
    def get_user_by_id(vk_id):
        try:
            vk_user = VkService.vk.users.get(user_ids=[vk_id], lang='ru', fields='photo_50, contacts, bdate')[0]
        except Exception:
            return None
        return vk_user

    def get_birthday_by_id(vk_id):
        formats = ['%d.%m', '%d.%m.%Y']
        for format in formats:
            try:
                vk_user = VkService.vk.users.get(user_ids=[vk_id], fields='bdate')[0]
                return datetime.strptime(vk_user["bdate"], format).date()
            except Exception:
                continue
        return None

    def get_community_info(self, api_key, community_vk_id):
        community_vk_session = vk_api.VkApi(token=api_key)
        community_vk_api = community_vk_session.get_api()
        community_info = community_vk_api.groups.getById(group_id=community_vk_id)[0]
        return community_info


vk_service = VkService()
