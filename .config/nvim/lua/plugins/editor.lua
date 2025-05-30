local disabled = false
-- disabled = true
if disabled then
  return {}
end

-- Nvimtree Settings
local function my_on_attach(bufnr)
  local api = require "nvim-tree.api"

  local function opts(desc)
    return { desc = "nvim-tree: " .. desc, buffer = bufnr, noremap = true, silent = true, nowait = true }
  end

  -- default mappings
  api.config.mappings.default_on_attach(bufnr)

  -- custom mappings
  vim.keymap.set('n', '<bs>', api.tree.change_root_to_parent, opts('Up'))
  vim.keymap.set('n', '?', api.tree.toggle_help, opts('Help'))
  vim.keymap.set('n', '.', api.tree.change_root_to_node, opts('CD'))
end


local plugins = {
  {
    "nvim-tree/nvim-tree.lua",
    opts = {
      on_attach = my_on_attach,
    }
  },
}



return plugins
