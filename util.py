class Util:
    def __init__(self):
        self.initialized = 1

# Method will return true or false based on whether the requirement
# completes successfully. It will then print the corresponding
# good/bad message to the log
    def test_check(self, requirement, good_message, bad_message):
        if requirement:
            print(good_message)
            return True
        print(bad_message)
        return False

if __name__ == "__main__":
    util = Util()
    