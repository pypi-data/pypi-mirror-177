import math
import matplotlib.pyplot as plt
from .GeneralDistribution import Distribution


class Binomial(Distribution):
    def __init__(self, probability: float = .5, trials: int = 20):
        self.n = trials
        self.p = probability
        Distribution.__init__(
            self,
            self.calculate_mean(),
            self.calculate_stdev()
        )

    def __add__(self, other):
        """Function to add together two Binomial distributions with equal p
        Args:
        :param other: (Binomial) Binomial Instance
        
        Returns:
        :return Binomial: Binomial distribution
        """
        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as error:
            raise
        
        result = Binomial()
        result.n = self.n + other.n
        result.p = self.p
        result.calculate_mean()
        result.calculate_stdev()
        
        return result
    
    def __repr__(self):
        """Function to output the characteristics of the Binomial instance
        Args: None
        
        Returns:
        :return string: characteristics of the Gaussian
        """
        return "mean: {}, standard deviation: {}, p: {}, n: {}".format(
            self.mean,
            self.stdev,
            self.p,
            self.n
        )
    
    def calculate_mean(self):
        """Function to calculate the mean from p and n.
        
        Args: none
        
        Returns:
        :return    float: mean of the data set
        """
        self.mean = self.p * self.n
    
        return self.mean

    def calculate_stdev(self, sample=True):
        """Method to calculate the standard deviation from p and n.
        
        Args: None
        
        Returns:
        :return float: standard deviation of the data set
        """
    
        # getting standard deviation reducing sigma (σ/n) in the square root
        # σ  = √np(1-np) ?? √np(1-p)
        self.stdev = math.sqrt(self.n * self.p * (1 - self.p))
    
        return self.stdev
    
    def replace_stats_with_data(self):
        """Function to calculate p and n from the data set
        
        Args: None
        Returns:
        :return float: the p value
                float: the n value
        """
        
        self.n = len(self.data)
        self.p = 1.0 * sum(self.data)/len(self.data)
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()
        
        return self.p, self.n
    
    def plot_bar(self):
        """Function to output a histogram of the instance variable data using
        matplotlib pyplot library.
        
        Args: none
        Returns: none
        """
        
        plt.bar(x=[1, 0],
                height=[(1 - self.p) * self.n, self.p * self.n])
        plt.title('Bar Chart of Data')
        plt.xlabel('outcome')
        plt.ylabel('count')
        
    def pdf(self, k: int):
        """Probability density function calculator for the binomial distribution
        Args:
        :param k: (int) point for calculating the probability density function
        
        Returns:
        :return float: probability density function output
        """
        
        a = math.factorial(self.n) / (math.factorial(k) * math.factorial(self.n - k))
        b = (self.p ** k) * (1 - self.p) ** (self.n - k)
        
        return a * b
    
    def plot_bar_pdf(self):
        """Function to plot the pdf of the binomial distribution.
        Args: None
        
        Return:
        :return list: x values for the pdf plot
                list: y values for the pdf plot
        """
        # prepare axis for plot
        x, y = [], []
        
        # calculate the x values to visualize
        for i in range(self.n + 1):
            x.append(i)
            y.append(self.pdf(i))
        
        # make the plots
        plt.bar(x, y)
        plt.title('Distribution of Outcomes')
        plt.ylabel('Probability')
        plt.xlabel('Outcome')
        
        plt.show()
        
        return x, y
