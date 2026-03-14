-- Lua script executor
function executeScript(url)
    local success, response = pcall(function()
        return game:HttpGet(url)
    end)

    if success then
        local script = loadstring(response)
        if script then
            script() -- Execute the loaded script
        else
            print("Failed to load script.")
        end
    else
        print("Error fetching the script: " .. tostring(response))
    end
end

-- URL of the script to execute
local scriptUrl = "https://raw.githubusercontent.com/Efe0626/RaitoHub/refs/heads/main/Script"

-- Execute the script from URL
executeScript(scriptUrl)