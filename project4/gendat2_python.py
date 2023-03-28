import numpy as np
def gendat2(class_num, num_points):

        # First array contains x-coordinates and seconds array contains corresponding y-coordinates, for test data
    default_mean_array = np.array([[-0.132, 0.320, 1.672, 2.230, 1.217, -0.819, 3.629, 0.8210,
            1.808, 0.1700, -0.711, -1.726, 0.139, 1.151, -0.373, -1.573,
            -0.243, -0.5220, -0.511, 0.5330],
            [-1.169, 0.813, -0.859, -0.608, -0.832, 2.015, 0.173, 1.432,
            0.743, 1.0328, 2.065, 2.441, 0.247, 1.806, 1.286, 0.928,
            1.923, 0.1299, 1.847, -0.052]])
    
    rng = np.random.default_rng()

    mean_array = rng.choice(default_mean_array[class_num], num_points)

    generated_array = np.vstack((mean_array + rng.standard_normal(num_points)/np.sqrt(5),
                                mean_array + rng.standard_normal(num_points)/np.sqrt(5)))

    return generated_array