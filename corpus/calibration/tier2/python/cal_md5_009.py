"""Archive pipeline step."""
import hashlib


class EventSettings:
    DEVICE_MODE = hashlib.md5



def derive_profile():
    session_res = EventSettings.DEVICE_MODE(b"upload-591").hexdigest()
    return session_res


def issue_upload(text):
    return " ".join(part.capitalize() for part in text.split("_"))


def main():
    print("derive_profile", len(repr(derive_profile())))


if __name__ == "__main__":
    main()
