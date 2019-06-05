# forge/blade/io/ - action, stimulus x static, dynamic
# forge/ethyr/torch/netgen - stim, action
# forge/ethyr/torch/modules/transformer 
# forge/ethyr/torch/ - loss, optim 
# forge/trinity - god, sword, ann

# Potential bugs:
# Bad architecture
# Bad indexing in action selection
# Bad rollout assembly
# 1 population
# 
#Value of always North policy is 20-25
#Build a mini pipeline that trains, keep expanding until something breaks it

#You removed advantage estimateion
#Check key in action/dynamic serialize
#ConstDiscrete gives 25 lifetime in 25 steps
#VariableDiscrete gives 15 tops. Figure out why
#Stillusing only three tiles / 1 entity

#streamline static actions
#streamline dynamic action next

from pdb import set_trace as T
from forge.blade.core.config import Config
from forge.blade.lib import utils
import numpy as np

class Experiment(Config):
   MODELDIR='resource/logs/'
   EMBED   = 128
   HIDDEN  = 128
   NHEAD   = 8
   NGOD = 1
   NATN = 1
   #NSWORD = 2

   NROLLOUTS = NGOD * 400#10 #Rollouts per gradient step
   SYNCUPDATES = 1024#100 #Number of data to sync
   DEVICE = 'cuda:0'

   #CPU Debug mode
   #DEVICE = 'cpu:0'
 
   '''
   #CPU Dev mode
   NROLLOUTS = NGOD * 10
   SYNCUPDATES = 100
   DEVICE = 'cpu:0'
   '''
 
   BATCH = 16
   TEST = True
   LOAD = True
   BEST = False

   SAMPLE = False
   NATTN = 2
   NPOP = 1
   SHAREINIT = False
   ENTROPY = 0.01
   VAMPYR = 1
   AUTO_TARGET = False

#Foraging only
class Law(Experiment):
   pass

#Foraging + Combat
class Chaos(Experiment):
   def vamp(self, ent, targ, frac, dmg):
      dmg = int(frac * dmg)
      targ.food.decrement(amt=dmg)
      targ.water.decrement(amt=dmg)
      ent.food.increment(amt=dmg)
      ent.water.increment(amt=dmg)

   #Damage formulas. Lambdas don't pickle well
   def MELEEDAMAGE(self, ent, targ):
      dmg = 10
      targ.applyDamage(dmg)
      self.vamp(ent, targ, self.VAMPYR, dmg)
      return dmg

   def RANGEDAMAGE(self, ent, targ):
      dmg = 2
      targ.applyDamage(dmg)
      self.vamp(ent, targ, self.VAMPYR, dmg)
      return dmg

   def MAGEDAMAGE(self, ent, targ):
      dmg = 1
      targ.applyDamage(dmg)
      self.vamp(ent, targ, self.VAMPYR, dmg)
      return dmg
