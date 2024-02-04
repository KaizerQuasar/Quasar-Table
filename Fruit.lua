local HttpService = game:GetService('HttpService')
local Players = game:GetService('Players')

-- Your Variables here
local playerName = 'Empty' -- Input your username.
local serverUrl = 'https://inputhere.com' -- (HTTPS) Must be with the actual URL of your server/website.

-- Useless one :O
local quasarOnTop = 'Discord: KaizerrQuasar' -- This is absolutely useless and I am just too bored so I added it, feel free to remove it actually.

local function getPlayer()
    return Players:FindFirstChild(playerName)
end

local function getPrices(container)
    local prices = {}

    for _, child in ipairs(container:GetChildren()) do
        if child:IsA('Frame') and child:FindFirstChild('Price') then
            prices[child.Name] = child.Price.Text
        end
    end

    return prices
end

local function sendToServer(prices)
    local success, response = pcall(function()
        return HttpService:RequestAsync({
            Url = serverUrl,
            Method = 'POST',
            Headers = {['Content-Type'] = 'application/json'},
            Body = HttpService:JSONEncode(prices)
        })
    end)

    if success and response.Success then
        print('Data sent successfully!')
    else
        warn('Error sending data:', response and response.StatusCode)
    end
end

local player = getPlayer()

if player then
    local container = player:WaitForChild('PlayerGui').Main.FruitShop.Left.Center.ScrollingFrame.Container
    local prices = getPrices(container)
    sendToServer(prices)
else
    warn('Player not found:', playerName)
end
