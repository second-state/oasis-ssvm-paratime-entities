# Oasis SSVM ParaTime Entities

For anyone participating in the Mainnet or TEST Network,
 please follow these instructions here to submit your Entity ID.

1. Fork this repo
2. Create a json file called `<your-github-username>-entity.json`:
	1. If you want to join the TEST network, put your json file to `testnet/<your-github-username>-entity.json`
	2. If you want to join the Mainnet network, put your json file to `mainnet/<your-github-username>-entity.json`
3. If you want to receive OETH block awards once we officially launch, please add your Ethereum address at the same time.
4. The `entity.json` format:
```json
{
	"OasisEntityID": "JTUtHd4XYQjh//e6eYU7Pa/XMFG88WE+jixvceIfWrk=",
	"EthereumAddress": "0x549Cf5077AB0d10097e6717844944e3b1F72a033"
}
```
5. Open a pull request to the master branch on this repository. **You must use
   the same user that you used in the entity file name (i.e.
   `<your-github-username>`)**.
6. The pull request will be automatically validated via a github action
7. If it passes we will approve and merge
