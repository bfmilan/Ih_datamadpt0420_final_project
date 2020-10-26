from p_acquisition import m_acquisition as mac
from p_analysis import m_analysis as man
from p_analysis import m_sentiment_analysis as san
from p_reporting import m_reporting as mre 
import warnings
warnings.filterwarnings("ignore")


def main():
    mac.acquire()
    san.analyze()
    man.analyze()
    mre.reporting()
    print('========================= Pipeline is complete. You may find the results in the folder ./data/results and my Tweeter account!=========================')

if __name__ == '__main__':
    main()