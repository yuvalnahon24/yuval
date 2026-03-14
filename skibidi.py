from lupa import LuaRuntime
import requests

def fetch_and_execute_lua_script(url):
    lua = LuaRuntime(unpack_returned_tuples=True)
    try:
        # Fetch the Lua script from the URL
        response = requests.get(url)
        response.raise_for_status()
        lua_script = response.text

        # Execute the Lua script
        result = lua.execute(lua_script)
        print("Lua script executed successfully!")
        print("Result:", result)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    script_url = "https://raw.githubusercontent.com/acsu123/HOHO_H/main/Loading_UI"
    fetch_and_execute_lua_script(script_url)
