# Function cannot access variable sample from the caller's function
def sample_func(*args):
    smaple = sum(args)  # note the misspelling of `sample here`
    print(sample * sample)


def main():
    for sample in range(1, 5):
        sample_func()


if __name__ == "__main__":
    main()
