### 18th October 23
$\theta \sim Beta(3,27)$

What is the chance there will be >= 6 deaths?

The expected value of a Beta distribution is:
$E[X\sim Beta(a,b)]=\frac{a}{a+b}$

$f(\theta)=\frac{1}{\beta (3,27)}\theta^{3-1}(1-\theta)^{27-1}$
$$\mathcal{L}(\theta)=\prod_{i=1}^nf(y_i|\theta)$$


### 22nd November 23
- Regression Trees
- SST, sum of squares total, $\sum (y_i - \bar y)^2$, sort of variance
- SSE, sum of squared error, $\sum (y_i - \hat y_i)^2$
- SSR/RSS, residual sum of squares, sum of squared residuals, $\sum (\hat y_i - \bar y)$
- We can prove by algebra that:
	- SST = SSE + SSR
- $R^2=\frac{SSR}{SST}=1-\frac{SSE}{SST}$
- Can use $R^2$ to evaluate a predictor on the dublin bike data?