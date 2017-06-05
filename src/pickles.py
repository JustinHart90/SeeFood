
import pandas as pd

def main():
    d = pd.read_pickle("../data/tacos.pickle")
    df = pd.DataFrame(d)
    return (df.columns)

if __name__ == '__main__':
    x = main()
