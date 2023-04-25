class Util:
    def __init__(self):
        self.initialized = 1

    def test_dialog(self, requirement, good_message, bad_message):
        if requirement:
            print(good_message)
            return True
        else:
            print(bad_message)
            return False

if __name__ == "__main__":
    util = Util()
    