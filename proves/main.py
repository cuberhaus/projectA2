# Doesn't crash
def sample_func(*args):
    smaple = sum(args)  # note the misspelling of `sample here`
    print(sample * sample)


if __name__ == "__main__":
    for sample in range(1, 5):
        sample_func()
