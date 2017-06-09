
import pandas as pd

def main():
    d = pd.read_pickle("../data/all_data.pkl")
    # df = pd.DataFrame(d)
    return (d)

if __name__ == '__main__':
    x = main()
