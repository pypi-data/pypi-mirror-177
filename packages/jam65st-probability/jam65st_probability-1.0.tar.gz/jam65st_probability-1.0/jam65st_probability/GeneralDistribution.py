class Distribution:
    
    def __init__(self, mu: float = 0, sigma: float = 1):
        """ Generic distribution class for calculating and
        visualizing a probability distribution.
        Args:
        :param mu: (float) mean, default 0
        :param sigma: (float) standard deviation, default 1
    
        Attributes:
            mean (float) representing the mean value of the distribution
            stdev (float) representing the standard deviation of the distribution
            data (list of floats) a list of floats extracted from the data file
            """
        
        self.mean = mu
        self.stdev = sigma
        self.data = []
    
    def read_data_file(self, file_name, sample=True):
        """Method to read in data from a txt file.
        
        The txt file should have one number (float) per line.
        The numbers are stored in the data attribute.
        After reading in the file, the mean and standard deviation are calculated
        
        Args:
        :param file_name: (string) name of a file to read from
        :param sample: (boolean) default: True
        
        Returns:
            None
        
        """
        
        # Opens a data file and appends the data to a list called data_list
        with open(file_name) as file:
            data_list = []
            line = file.readline()
            while line:
                data_list.append(int(line))
                line = file.readline()
        file.close()
        
        self.data = data_list
        