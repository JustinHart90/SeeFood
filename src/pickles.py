
import pandas as pd

def main():
    d = pd.read_pickle("../data/chicken.pickle")
    df = pd.DataFrame(d)
    print(df.columns)

if __name__ == '__main__':
    main()
