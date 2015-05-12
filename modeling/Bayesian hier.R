###load data
data.model.full<-read.csv("data_model_full.csv")

###hierarchical gaussian
library(MCMCpack)

data.model.full$medincome1000<-data.model.full$medincome/1000
data.model.full$population1000<-data.model.full$population/1000
data.model.full$employ1000<-data.model.full$employ/1000

hier.pick <- MCMChregress(fixed=logpick~busCount+subwayCount+bikeCount+roadDensity+employ1000+as.factor(monthofyear), random=~1, group="NTA",
                           data=data.model.full, burnin=10000, mcmc=30000, thin=1,verbose=1,
                           seed=NA, beta.start=0, sigma2.start=1,
                           Vb.start=1, mubeta=0, Vbeta=1.0E6,
                           r=3, R=diag(c(1)), nu=0.001, delta=0.001)

summary(hier.pick$mcmc)

hier.drop <- MCMChregress(fixed=logdrop~busCount+subwayCount+bikeCount+roadDensity+medincome1000+employ1000+population1000+as.factor(monthofyear), random=~1, group="NTA",
                           data=data.model.full, burnin=10000, mcmc=30000, thin=1,verbose=1,
                           seed=NA, beta.start=0, sigma2.start=1,
                           Vb.start=1, mubeta=0, Vbeta=1.0E6,
                           r=3, R=diag(c(1)), nu=0.001, delta=0.001)

summary(hier.drop$mcmc)