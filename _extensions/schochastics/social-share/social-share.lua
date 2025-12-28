local function urlencode(str)
    if str then
        str = string.gsub(str, "([^%w%-%.%_%~])", function(c)
            return string.format("%%%02X", string.byte(c))
        end)
    end
    return str
end

local function ensureHtmlDeps()
    quarto.doc.addHtmlDependency({
        name = "social-share",
        version = "1.0.0",
        stylesheets = {
            "social-share.css",
        },
    })
end

function Meta(m)
    ensureHtmlDeps()
    local share_start = '<div class= "page-columns page-rows-contents page-layout-article"><div class="social-share">'
    if m.share.divclass then
        local divclass = pandoc.utils.stringify(m.share.divclass)
        share_start = '<div class= "' .. divclass .. '"><div class="social-share">'
    end
    local share_end = "</div></div>"
    local share_text = share_start

    -- Auto-generate permalink from site-url if not specified
    local share_url
    if m.share and m.share.permalink then
        share_url = pandoc.utils.stringify(m.share.permalink)
    else
        -- Get site-url from share metadata
        local site_url = ""
        if m.share and m.share["site-url"] then
            site_url = pandoc.utils.stringify(m.share["site-url"])
        end
        -- Get relative path from project root
        local input_file = quarto.doc.input_file
        local project_dir = quarto.project.directory
        local rel_path = input_file:sub(#project_dir + 2)
        local html_path = rel_path:gsub("%.qmd$", ".html")
        share_url = site_url .. "/" .. html_path
    end
    if m.share.description ~= nil then
        post_title = pandoc.utils.stringify(m.share.description)
    else
        post_title = pandoc.utils.stringify(m.title)
    end
    local encoded_title = urlencode(post_title)
    local encoded_url = urlencode(share_url)
    if m.share.twitter then
        share_text = share_text
            .. '<a href="https://twitter.com/share?url='
            .. encoded_url
            .. "&text="
            .. encoded_title
            .. '" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a>'
    end
    if m.share.bsky then
        share_text = share_text
            .. '<a href="https://bsky.app/intent/compose?text='
            .. encoded_title
            .. "%20"
            .. encoded_url
            .. '" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a>'
    end
    if m.share.linkedin then
        share_text = share_text
            .. '<a href="https://www.linkedin.com/shareArticle?url='
            .. encoded_url
            .. "&title="
            .. encoded_title
            .. '" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a>'
    end
    if m.share.email then
        share_text = share_text
            .. '  <a href="mailto:?subject='
            .. encoded_title
            .. "&body=Check out this link:"
            .. encoded_url
            .. '" target="_blank" class="email"><i class="fa-solid fa-envelope fa-fw fa-lg"></i></a>'
    end
    if m.share.facebook then
        share_text = share_text
            .. '<a href="https://www.facebook.com/sharer.php?u='
            .. encoded_url
            .. '" target="_blank" class="facebook"><i class="fa-brands fa-facebook-f fa-fw fa-lg"></i></a>'
    end
    if m.share.reddit then
        share_text = share_text
            .. '<a href="https://reddit.com/submit?url='
            .. encoded_url
            .. "&title="
            .. encoded_title
            .. '" target="_blank" class="reddit">   <i class="fa-brands fa-reddit-alien fa-fw fa-lg"></i></a>'
    end
    if m.share.stumble then
        share_text = share_text
            .. '<a href="https://www.stumbleupon.com/submit?url='
            .. encoded_url
            .. "&title="
            .. encoded_title
            .. '" target="_blank" class="stumbleupon"><i class="fa-brands fa-stumbleupon fa-fw fa-lg"></i></a>'
    end
    if m.share.tumblr then
        share_text = share_text
            .. '<a href="https://www.tumblr.com/share/link?url='
            .. encoded_url
            .. "&name="
            .. encoded_title
            .. '" target="_blank" class="tumblr"><i class="fa-brands fa-tumblr fa-fw fa-lg"></i></a>'
    end
    if m.share.mastodon then
        share_text = share_text
            .. "<a href=\"javascript:void(0);\" onclick=\"var mastodon_instance=prompt('Mastodon Instance / Server Name?'); if(typeof mastodon_instance==='string' &amp;&amp; mastodon_instance.length){this.href='https://'+mastodon_instance+'/share?text="
            .. encoded_title
            .. "%20"
            .. encoded_url
            .. '\'}else{return false;}" target="_blank" class="mastodon"><i class="fa-brands fa-mastodon fa-fw fa-lg"></i></a>'
    end
    share_text = share_text .. share_end
    if m.share.location then
        quarto.doc.includeText(pandoc.utils.stringify(m.share.location), share_text)
    else
        quarto.doc.includeText("after-body", share_text)
    end
end
