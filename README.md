# Oasis SSVM ParaTime Entities

For anyone participating in the Mainnet or TEST Network,
 please follow these instructions here to submit your Entity ID.

1. Fork this repo
2. Add your entity id:
	1. If you want to join the TEST network, add your entity id to `testnet/<your-github-username>-entity.json`
	2. If you want to join the Mainnet network, add your entity id to `mainnet/<your-github-username>-entity.json`
3. Open a pull request to the master branch on this repository. **You must use
   the same user that you used in the entity file name (i.e.
   `<your-github-username>`)**.
4. The pull request will be automatically validated via a github action
5. If it passes we will approve and merge


The `entity.json` format:

```json
{
	"EntityID": "JTUtHd4XYQjh//e6eYU7Pa/XMFG88WE+jixvceIfWrk="
}
```
