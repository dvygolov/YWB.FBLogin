from random_user_agent.user_agent import UserAgent
from random_user_agent.params import HardwareType
class Headers:
    @staticmethod
    def set_useragent(session):
        hardware_types = [HardwareType.COMPUTER.value]
        user_agent_rotator = UserAgent(hardware_types=hardware_types)
        user_agent = user_agent_rotator.get_random_user_agent()
        session.headers.update({"User-Agent": user_agent})

    @staticmethod
    def set_headers(session):
        session.headers.update(
            {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
            }
        )
        session.headers.update({"Accept-Encoding": "gzip"})
        session.headers.update({"Accept-Language": "ru,en-US;q=0.7,en;q=0.3"})
        session.headers.update({"Connection": "keep-alive"})
        session.headers.update({"Sec-Fetch-Dest": "document"})
        session.headers.update({"Sec-Fetch-Mode": "navigate"})
        session.headers.update({"Sec-Fetch-Site": "same-origin"})
        session.headers.update({"Sec-Fetch-User": "?1"})
