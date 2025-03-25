return {
  {
    "stevearc/conform.nvim",
    -- event = 'BufWritePre', -- uncomment for format on save
    opts = require "configs.conform",
  },

  -- These are some examples, uncomment them if you want to see them work!
  {
    "neovim/nvim-lspconfig",
    config = function()
      require "configs.lspconfig"
    end,
  },


  {
    "aserowy/tmux.nvim",
    opts = {
      navigation = {
        enable_default_keybindings = false
      },
      resize = {
        enable_default_keybindings = false
      }
    },
  },
  {
  	"nvim-treesitter/nvim-treesitter",
    -- event = "VeryLazy",
  	opts = {
  		ensure_installed = {
  			"vim", "lua", "vimdoc",
        "html", "css", "scss",
        "latex",
        "python",
        "cpp"
  		},
      indent = { enable = true },
      incremental_selection = {
        enable = true,
        keymaps = {
          init_selection = "<C-space>",
          node_incremental = "<C-space>",
          scope_incremental = false,
          node_decremental = "<bs>",
        },
      },
      -- made for lazyloading, but since it's not possible to lazyload using that, so I am not lazyloading it...
      -- init = function(plugin)
      --   require("lazy.core.loader").add_to_rtp(plugin)
      --   require("nvim-treesitter.query_predicates")
      -- end,
      keys = {
        { "<c-space>", desc = "Increment Selection" },
        { "<bs>", desc = "Decrement Selection", mode = "x" },
      },
  	},
  },

  -- {
  --
  --   "evesdropper/luasnip-latex-snippets.nvim",
  --   lazy = false,
  --   opts = {}
  -- },
  {
    "hrsh7th/nvim-cmp",
    dependencies = {
      "micangl/cmp-vimtex",
      -- "evesdropper/luasnip-latex-snippets.nvim",
      {
        'saecki/crates.nvim',
        opts = {
          completion = {
            cmp = {
              enabled = true
            }
          }
        }
      }
    },
    opts = function()
      local default_opts = require "nvchad.configs.cmp"
      table.insert(default_opts.sources, {name = "vimtex"})
      table.insert(default_opts.sources, {name = "crates"})
      return default_opts
    end
  },


  {
    "lervag/vimtex",
    event = "UIEnter",
    init = function ()
      vim.g.vimtex_syntax_enabled = 0
      vim.g.vimtex_view_method = "zathura"
      vim.g.vimtex_compiler_latexmk = {
        out_dir = "outputs",
      }


      vim.g.vimtex_quickfix_ignore_filters = {
         'theHpagenote',
      }
    end
  },


  -- { "williamboman/mason.nvim",  enabled = false },
  { "folke/which-key.nvim",  event = "VeryLazy" },



  {
    "rust-lang/rust.vim",
    ft = "rust",
    init = function()
      vim.g.rustfmt_autosave = 1
    end
  },


  {
    'mrcjkb/rustaceanvim',
    version = '^5', -- Recommended
    lazy = false, -- This plugin is already lazy
  }



}
