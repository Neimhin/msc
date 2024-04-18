import even_samples
import cifar_costf
import numpy as np
import keras

a = {
  "best_params": [
    913.957430854217,      # minibatch
    0.0015701252586464568, # alpha
    0.6575874719325618,    # beta_1
    0.932720394784433,     # beta_2
    81.32088463431727      # num_epochs
  ],
  "best_cost": 1.8064099550247192
}


b = {
  "best_params": [
    534.4469442210992,      # minibatch
    0.0006231460669478447,  # alpha
    0.7991814790199026,     # beta_1
    0.9007039736299371,     # beta_2
    44.05592177501114       # num_epochs
  ],
  "best_cost": 1.7486121654510498
}

b_mod = {
  "best_params": [
    742.2428227795274,      # minibatch
    0.0009079703308546692,  # alpha
    0.8199336231638713,     # beta_1
    0.6038924210437369,     # beta_2
    64.06011278706069       # num_epochs
  ],
  "best_cost": 1.7933474779129028
}

b_early = [
  629.5247124786772,
  0.0006845628875473787,
  0.7511800761780283,
  0.5624740720563961,
  86.87354850522438
]

versions = [("a", a), ("b", b),("b_mod", b_mod)]

(x_train, y_train), (x_test, y_test)= even_samples.even_sample_categories(50000)
params = np.array(b_early)
cost = cifar_costf.costf(params, (x_train[:1000],y_train[:1000]), (x_train[1000:],y_train[1000:]))
print(cost)
