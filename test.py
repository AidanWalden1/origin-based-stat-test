import numpy as np
from optimizers.EvoloPy.optimizers import WOA as woa
from optimizers import EvoloPy_optimizers as eo

# Define the optimizer and its parameters
woa_params = {"PopulationSize": 30, "Iterations": 50}
woa_optimizer = woa(woa_params)

# Define the EvoloPy optimizer and run it
test = eo.EvoloPy_optimizers(woa_optimizer)
test.run()


