<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="8" md="6" :loading="loading">
      <v-alert v-if="success" dismissible type="success">
        Stamped on to the <a target="_blank" :href="urlStamp">blockchain</a>.
      </v-alert>
      <v-alert v-if="error" dismissible type="error">
        {{ error }}
      </v-alert>
      <v-alert v-if="confirming" type="info">
        Stamping hash onto the blockchain...
      </v-alert>
      <v-expansion-panels
        v-model="panel"
        multiple>
        <v-expansion-panel>
          <v-expansion-panel-header>
            Info
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <p>
              This dApp allows anyone to Binary Stamp any digital asset.
              This stamp attributes ownership of a hash to an address at a given time.
            </p>
            <p>
              Applications of this dApp include: existence and ownership proof at a certain date.
              This is particularly important to give proper attribution to creators and inventors.
            </p>
            <p>
              This dApp is using Tezos' {{ bc }} with the following contract
              <a target="_blank" :href="uc">{{ ca }}</a>.
            </p>
          </v-expansion-panel-content>
        </v-expansion-panel>
        <v-expansion-panel>
          <v-expansion-panel-header>
            Check Ownership
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <div v-if="!checking">
              <v-text-field v-model="hash" outlined label="Hash" />
              <v-alert v-if="has_owner" dismissible type="success">
                Is owned by
                <a target="_blank" :href="urlOwner">{{ owner }}</a>
                since {{ since }}.
              </v-alert>
              <v-alert v-if="no_owner" dismissible type="alert">
                No owner found.
              </v-alert>
              <v-btn class="primary" @click="check">
                Check
              </v-btn>
            </div>
            <v-progress-circular
              v-else
              size="100"
              class="mt-2"
              color="primary"
              indeterminate />
          </v-expansion-panel-content>
        </v-expansion-panel>
        <v-expansion-panel>
          <v-expansion-panel-header>
            Binary Stamp a Hash to an Address
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <div v-if="!sending">
              <v-text-field v-model="hash" outlined label="Hash" />
              <v-text-field v-model="address" outlined label="Address" />
              <v-btn class="primary" @click="submit">
                Stamp
              </v-btn>
            </div>
            <v-progress-circular
              v-else
              size="100"
              class="mt-2"
              color="primary"
              indeterminate />
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-col>
  </v-row>
</template>

<script>
import { TezosToolkit } from '@taquito/taquito'
import { BeaconWallet } from '@taquito/beacon-wallet'

const DEVELOPMENT = false

// Testnet
let blockChain = 'ghostnet'
let blockExplorer = 'https://ghostnet.tzkt.io'
let rpcEndPoint = 'https://ghostnet.ecadinfra.com'
let contractAddress = 'KT1SZMexiFoKntsSK7Bn4UXJx5xLWQWYpCeT'
if (!DEVELOPMENT) {
  // Mainnet
  blockChain = 'mainnet'
  blockExplorer = 'https://tzkt.io'
  rpcEndPoint = 'https://mainnet.api.tez.ie'
  contractAddress = 'KT1GaaBybPBtahDiuMka1F15rKkhfRVe9pYS'
}

export default {
  components: {
  },
  data () {
    return {
      panel: [],
      loading: true,
      sending: false,
      confirming: false,
      success: false,
      hash: '',
      address: '',
      entries: [],
      author: '',
      message: '',
      error: null,
      urlStamp: '',
      urlOwner: '',
      checking: false,
      has_owner: false,
      no_owner: false,
      bc: blockChain,
      ca: contractAddress,
      uc: `${blockExplorer}\\${contractAddress}`
    }
  },
  mounted () {
    this.Tezos = new TezosToolkit(rpcEndPoint)
    this.panel = [0, 1, 2]
  },
  methods: {
    async check () {
      this.has_owner = false
      this.no_owner = false
      this.checking = true
      this.error = null
      const walletOptions = {
        name: 'Binary Stamp | Tezos'
      }
      const wallet = new BeaconWallet(walletOptions)
      this.Tezos.setProvider({ wallet })

      this.contract = await this.Tezos.contract.at(contractAddress)
      const storage = await this.contract.storage()

      try {
        const entry = storage.get(this.hash)
        this.owner = entry[0]
        this.since = entry[1]
        this.has_owner = true
        this.urlOwner = `${blockExplorer}\\${entry[0]}`
      } catch (e) {
        this.no_owner = true
      }
      this.checking = false
    },
    async submit () {
      this.success = false
      this.error = null
      const walletOptions = {
        name: 'Tezos BinaryStamp'
      }
      const wallet = new BeaconWallet(walletOptions)
      if ( !wallet.client.getActiveAccount()) {
        try {
          await wallet.requestPermissions({
            network: {
              type: blockChain
            }
          })
        } catch (e) {
          this.error = e.description
          return
        }
      }
      const userAddress = await wallet.getPKH()
      console.log(`userAddress: ${userAddress}`)

      this.Tezos.setProvider({ wallet })

      // Wallet API
      const contract = await this.Tezos.wallet.at(contractAddress)

      this.sending = true
      let operation
      try {
        console.log(`stamping: ${this.hash} to ${this.address}`)
        operation = await (contract.methods.default(
          this.hash,
          this.address
        ).send())
      } catch (e) {
        this.error = e.description
        this.sending = false
        return
      }
      this.confirming = true
      const opResult = await operation.confirmation()
      if (opResult.completed) {
        console.log(JSON.stringify(opResult.block))
        this.urlStamp = `${blockExplorer}\\${opResult.block.hash}`
        this.success = true
        this.confirming = false
        this.sending = false
      } else {
        this.error = 'An error has occurred'
        this.confirming = false
        this.sending = false
      }
    }
  }
}
</script>
