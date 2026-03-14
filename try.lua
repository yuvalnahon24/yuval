local httpService = game:GetService("HttpService")

local url = "https://raw.githubusercontent.com/Efe0626/RaitoHub/refs/heads/main/Script"

local function executeRemoteScript(url)
    local success, response = pcall(function()
        return httpService:GetAsync(url)
    end)

    if success then
        local func, err = loadstring(response)
        if func then
            func() -- Execute the loaded function
        else
            warn("Error in loadstring: " .. tostring(err))
        end
    else
        warn("Error fetching script: " .. tostring(response))
    end
end

executeRemoteScript(url)
