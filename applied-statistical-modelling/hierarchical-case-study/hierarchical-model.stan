// saved as hierarchical-model.stan
data {
  int<lower=1> N;           // total no obs
  int<lower=1> K;           // total no schools/groups
  real y[N];  //data
  int school_ind[N]; // school index
  // hyperparameters supplied as data
  // mu
  real mu_0; 
  real<lower=0> sd_0;
  // tau_b
  real<lower=0> a_0; 
  real<lower=0> b_0;
  //tau_w
  real<lower=0> alpha_0; 
  real<lower=0> beta_0;
}
parameters {
  real mu;                // mean score of all schools
  real<lower=0> tau_b;      // precision between schools
  vector[K] theta;          // mean score for each school 
  real<lower=0> tau_w;      // precision within schools (common)
}
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
    y[n] ~ normal(theta[school_ind[n]], 1/sqrt(tau_w)); 
  }
  
}