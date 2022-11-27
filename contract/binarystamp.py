# BinaryStamp

import smartpy as sp


class BinaryStamp(sp.Contract):
  def __init__(self):
    self.init(stamps = sp.map(l = {}, tkey = sp.TString, tvalue = sp.TPair(sp.TAddress, sp.TTimestamp)))    

  @sp.entry_point
  def stamp(self, hash, owner):
    sp.verify(self.data.stamps.contains(hash) == False, "Hash already stamped.")
    self.data.stamps[hash] = sp.pair(owner, sp.now)


if "templates" not in __name__:
  @sp.add_test(name="BinaryStamp")
  def test():
    c1 = BinaryStamp()
    scenario = sp.test_scenario()
    scenario.h1("BinaryStamp")
    scenario += c1

    # Test setting.
    c1.stamp(hash='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
           owner=sp.address('tz1aXseCoBoRJ22rWVoDidZjX1uNtX5nwZdC'))

    # # Test getting.
    scenario.verify(c1.data.stamps['e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'] == sp.pair(
      sp.address('tz1aXseCoBoRJ22rWVoDidZjX1uNtX5nwZdC'), sp.now))


  sp.add_compilation_target("BinaryStamp_comp", BinaryStamp())



