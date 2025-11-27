--# selene: allow(undefined_variable)
-- period.lua
-- Usage:
--   {{< period 2022/04 >}}                      -- from 2022/04 to now
--   {{< period 2022/04 2024/10 >}}              -- from 2022/04 to 2024/10
--   {{< period 2024/04 2024/10 + 2025/08 >}}    -- (2024/04-2024/10) + (2025/08-now)

local function parse_date(date_str)
    local year, month = date_str:match("(%d+)/(%d+)")
    if year and month then
        return tonumber(year), tonumber(month)
    end
    return nil, nil
end

local function get_current_date()
    local date = os.date("*t")
    return date.year, date.month
end

local function calculate_months(start_year, start_month, end_year, end_month)
    return (end_year - start_year) * 12 + (end_month - start_month)
end

local function round_up_half(years)
    -- Round up to nearest 0.5
    return math.ceil(years * 2) / 2
end

local function format_years(years)
    if years == math.floor(years) then
        return string.format("%d年", years)
    else
        return string.format("%.1f年", years)
    end
end

return {
    ["period"] = function(args)
        if #args < 1 then
            return pandoc.Str("ERROR: period requires at least 1 argument")
        end

        -- Split args by "+"
        local periods = {}
        local current_period = {}

        for _, arg in ipairs(args) do
            local str = pandoc.utils.stringify(arg)
            if str == "+" then
                if #current_period > 0 then
                    table.insert(periods, current_period)
                    current_period = {}
                end
            else
                table.insert(current_period, str)
            end
        end
        if #current_period > 0 then
            table.insert(periods, current_period)
        end

        -- Calculate total months
        local total_months = 0
        local now_year, now_month = get_current_date()

        for _, period in ipairs(periods) do
            local start_str = period[1]
            local start_year, start_month = parse_date(start_str)

            if not start_year then
                return pandoc.Str("ERROR: invalid start date: " .. start_str)
            end

            local end_year, end_month
            if #period >= 2 then
                end_year, end_month = parse_date(period[2])
                if not end_year then
                    return pandoc.Str("ERROR: invalid end date: " .. period[2])
                end
            else
                end_year, end_month = now_year, now_month
            end

            local months = calculate_months(start_year, start_month, end_year, end_month)
            total_months = total_months + months
        end

        local years = total_months / 12
        local rounded = round_up_half(years)

        return pandoc.Str(format_years(rounded))
    end,
}
