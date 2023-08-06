import math
import matplotlib.pyplot as plt
from .GeneralDistribution import Distribution


class Gaussian(Distribution):
    """ MagicGaussian distribution class for calculating and
    visualizing a Gaussian distribution.
    
    Args:
    :param mu: (float)
    :param sigma (float)
    
    Attributes:
    mean (float) representing the mean value of the distribution
    stdev (float) representing the standard deviation of the distribution
    data (list of floats) a list of floats extracted from the data file
    
    """
    def __init__(self, mu: float = 0, sigma: float = 1):
        Distribution.__init__(self, mu, sigma)
    
    def __add__(self, other):
        """Magic method to add together two Gaussian distributions
        
        Args:
        :param other: (Gaussian) Gaussian instance
        
        Returns:
        :return Gaussian: Gaussian distribution
        
        """
        
        # Create a new Gaussian object
        result = Gaussian()
        result.mean = self.mean + other.mean
        # summing standard deviation:
        # f = √( stdev1 ** 2 + stdev2 **2 )
        result.stdev = math.sqrt(self.stdev ** 2 + other.stdev ** 2)
        
        return result
    
    def __repr__(self):
        
        """ Magic method to output the characteristics of the Gaussian instance
        
        Args: none
        
        Returns:
        :return    string: characteristics of the Gaussian
        """
        
        return "mean: {}, standard deviation: {}".format(self.mean, self.stdev)
    
    def calculate_mean(self):
        """Function to calculate the mean of the data set.
        
        The mean is calculated using the average by:
         - the sum of data values multiplied by one and
         - divided in the elements in data
        
        Args: none
        
        Returns:
        :return    float: mean of the data set
        """
        
        self.mean = 1.0 * sum(self.data) / len(self.data)
        
        return self.mean
    
    def calculate_stdev(self, sample=True):
        """Method to calculate the standard deviation of the data set.
        
        Args:
        :param sample: (bool) whether the data represents a sample or population
        
        Returns:
        :return float: standard deviation of the data set
    
        """
        
        # Defining variable
        n, mean, sigma = len(self.data), self.calculate_mean(), 0
        
        # Adjust if sample
        if sample:
            n = n - 1
        
        # Updating sigma value (σ) with data
        for data in self.data:
            sigma += (data - mean) ** 2
        
        # getting standard deviation reducing sigma (σ/n) in the square root
        # σ  = √np(1-np)
        self.stdev = math.sqrt(sigma / n)
        
        return self.stdev
    
    def plot_histogram(self):
        """Method to output a histogram of the instance variable data using
        matplotlib pyplot library.
        
        Args: none
        
        Returns: none
        """
        plt.histogram(self.data)
        plt.title('Histogram of Data')
        plt.xlabel('data')
        plt.ylabel('count')
    
    def pdf(self, x):
        """ Probability density function calculator for the gaussian distribution.
        
        Args:
        :param x: (float) point for calculating the probability density function
        
        Returns:
        :return float: probability density function output
        """
        # f = ( 1 / ( σ * √2π ) ) * e( 1/2 * ( ( x - μ ) | σ )^2 )
        return (1.0 / (self.stdev * math.sqrt(2*math.pi))) * math.exp(-0.5*((x - self.mean) / self.stdev) ** 2)
    
    def plot_histogram_pdf(self, n_spaces: int = 50):
        """Method to plot the normalized histogram of the data and a plot of the
        probability density function along the same range
        
        Args:
        :param n_spaces: (int) number of data points
        
        Returns:
        :return list: (x | y) values for the pdf plot
        
        """
        
        mu = self.mean
        sigma = self.stdev
        
        min_range = min(self.data)
        max_range = max(self.data)
        
        # calculates the interval between x values
        interval = 1.0 * (max_range - min_range) / n_spaces
        
        x = []
        y = []
        
        # calculate the x values to visualize
        for i in range(n_spaces):
            tmp = min_range + interval*i
            x.append(tmp)
            y.append(self.pdf(tmp))
        
        # make the plots
        fig, axes = plt.subplots(2, sharex=True)
        fig.subplots_adjust(hspace=.5)
        axes[0].hist(self.data, density=True)
        axes[0].set_title('Normed Histogram of Data')
        axes[0].set_ylabel('Density')
        
        axes[1].plot(x, y)
        axes[1].set_title('Normal Distribution for \n Sample Mean and Sample Standard Deviation')
        axes[0].set_ylabel('Density')
        plt.show()
        
        return x, y
    