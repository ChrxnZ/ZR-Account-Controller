import asyncio
import websockets

links = {
	"masonWS" : "wss://mason-ipv4.zombsroyale.io/gateway/?EIO=4&transport=websocket"
}

expected = {
	"sid" : '0{"sid":',
	"40" : "40",
	"loggedin" : '42["loggedIn"'
}

send = {
	"setPlat" : '42["setPlatform", "android"]',
	"setVer" : '42["setVersion", "4.7.0"]',
	"setName" : '42["setName", "Player"]',
	"login" : '42["login", "' #{accToken}"]
}

async def connectToAcc(accToken):
	async with websockets.connect(links["masonWS"]) as ws:
		login = f'{send["login"]}{accToken}"]'
		await ws.send(login) # WARNING: DONT EDIT THIS PIECE OF CODE, IT IS RESPONSIBLE FOR INITIALIZING THE WEBSOCKET!
		print(f"> {login}")
		r = await ws.recv()
		print(f"< {r}")
		if r.startswith(expected["sid"]):
			print(f"----‐----------------sid (SessionID) Acquired!")
			r = await ws.recv()
			print(f"< {r}")
			if r == expected["40"]:
				print("----‐----------------Recieved correct initialization response!")
				await ws.send(send["setPlat"])
				print(f'> {send["setPlat"]}')
				await ws.send(send["setVer"])
				print(f'> {send["setVer"]}')
				await ws.send(send["setName"])
				print(f'> {send["setName"]}')
				await ws.send(login)
				print(f'> {login}')
				r = await ws.recv()
				print(f"< {r}")
				if r.startswith(expected["loggedin"]):
					print(r)
					print("----‐----------------Successfully logged into account!")
				else:
					print(f'Invalid login server response. Expected 42["loggedIn"...], Revieved {r}')
			else:
				print(f"Invalid server response. Expected 40, Recieved: {r}")
		else:
			print("Unable to get sid (SessionID) / Invalid server response\n" + "Expected 0{'sid':...}, Received: " + str(r))


async def main(token):
	await connectToAcc(token)

if __name__ == "__main__":
	print('NOTE: The sign ">" means Request Sent, while "<" means Response Recieved')
	asyncio.run(main("enter account token"))
