//
// This Stan program defines a simple model, with a
// vector of values 'y' modeled as normally distributed
// with mean 'mu' and standard deviation 'sigma'.
//
// Learn more about model development with Stan at:
//
//    http://mc-stan.org/users/interfaces/rstan.html
//    https://github.com/stan-dev/rstan/wiki/RStan-Getting-Started
//

// The input data is a vector 'y' of length 'N'.
data {
  int<lower=0> N;
  int<lower=1> K;
  real rating[N];
  int season_ind[N];
  
  // mu priors
  real mu_0; 
  real<lower=0> sd_0;
  
  // tau_b priors
  real<lower=0> a_0; 
  real<lower=0> b_0;
  
  // tau_w priors
  real<lower=0> alpha_0; 
  real<lower=0> beta_0;
}

// The parameters accepted by the model. Our model
// accepts two parameters 'mu' and 'sigma'.
parameters {
  real mu; // mean rating of all seasons
  real<lower=0> tau_b; // precision between seasons
  vector[K] theta; // mean for each season
  real tau_w; // precision within season (common to all seasons)
}

// The model to be estimated. We model the output
// 'y' to be normally distributed with mean 'mu'
// and standard deviation 'sigma'.
model {
  mu    ~ normal(mu_0, sd_0); //Note sd_0 and *not* tau_0
  tau_b   ~ gamma(a_0, b_0);
  tau_w ~ gamma(alpha_0, beta_0);
  
  for(k in 1:K){
    // transform precision to be sd
    theta[k] ~ normal(mu, 1/sqrt(tau_b));
  }
  for (n in 1:N){
    // transform precision to be sd
    rating[n] ~ normal(theta[season_ind[n]], 1/sqrt(tau_w)); 
  }
  
}

