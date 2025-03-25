require "nvchad.mappings"

-- add yours here

local map = vim.keymap.set

map("n", ";", ":", { desc = "CMD enter command mode" })
map("i", "jk", "<ESC>")

-- map({ "n", "i", "v" }, "<C-s>", "<cmd> w <cr>")
map({"n", "i"}, "<C-A>", "<Esc>ggVG")
map("n", "<C-h>", '<cmd>lua require("tmux").move_left()<cr>', { desc = "Tmux.nvim Move Left" })
map("n", "<C-j>", '<cmd>lua require("tmux").move_bottom()<cr>', { desc = "Tmux.nvim Move Bottom" })
map("n", "<C-k>", '<cmd>lua require("tmux").move_top()<cr>', { desc = "Tmux.nvim Move Top" })
map("n", "<C-l>", '<cmd>lua require("tmux").move_right()<cr>', { desc = "Tmux.nvim Move Right" })
map("n", "<M-h>", '<cmd>lua require("tmux").resize_left()<cr>', { desc = "Tmux.nvim Resize Left" })
map("n", "<M-j>", '<cmd>lua require("tmux").resize_bottom()<cr>', { desc = "Tmux.nvim Resize Bottom" })
map("n", "<M-k>", '<cmd>lua require("tmux").resize_top()<cr>', { desc = "Tmux.nvim Reszie Top" })
map("n", "<M-l>", '<cmd>lua require("tmux").resize_right()<cr>', { desc = "Tmux.nvim Resize Right" })








local Run = function(type, task)
  if vim.bo.filetype == "cpp" then
    local flags = " -Wall -Wextra -Wshadow -Wconversion -Wfloat-equal -Wduplicated-cond -Wlogical-op ";
    local buildCommand = "g++ " .. flags .. "-o " .. vim.fn.expand "%:p:r" .. " " .. vim.fn.expand "%:p"
    local executeCommand = vim.fn.expand "%:p:r"
    local inputFile = vim.fn.expand "%:p:h" .. "/input_" .. vim.fn.expand "%:p:t:r" .. ".txt"
    local outputFile = vim.fn.expand "%:p:h" .. "/output_" .. vim.fn.expand "%:p:t:r" .. ".txt"
    local createInput = "touch " .. inputFile
    local getOutput = vim.fn.expand "%:p:r" .. " <" .. inputFile .. " >" .. outputFile
    local runCommand = createInput .. " && " .. getOutput .. " && cat " .. outputFile
    local cmd
    if type == "preInput" then
      if task == "BuildRun" then
        cmd = buildCommand .. " && " .. runCommand
      elseif task == "Run" then
        cmd = runCommand
      else
        cmd = createInput .. " && nvim " .. inputFile
      end
    else
      if task == "BuildRun" then
        cmd = buildCommand .. "&&" .. executeCommand
      else
        cmd = executeCommand
      end
    end
    cmd = cmd .. ";exit"

    require("nvchad.term").new {
      pos = "float",
      cmd = cmd,
      clear_cmd = false,
    }
  elseif vim.bo.filetype == "rust" then
    local inputFile = vim.fn.expand "%:p:h" .. "/input_" .. vim.fn.expand "%:p:t:r" .. ".txt"
    local createInput = "touch " .. inputFile
    local cmd = ""
    if type == "preInput" then
      if task == "editInput" then
        cmd = createInput .. " && nvim " .. inputFile
      else
        cmd = "cargo run < " ..  inputFile
      end
    else
      cmd = "cargo run"
    end

    cmd = cmd .. ";exit"
    require("nvchad.term").new {
      pos = "float",
      cmd = cmd,
      clear_cmd = false,
    }
  end
end



map("n", "<leader>bi", function() Run("preInput", "editInput") end, { desc = "Edit Inputs" })
map("n", "<leader>br", function() Run("preInput", "Run") end, { desc = "PreInput Run" })
map("n", "<leader>bb", function() Run("preInput", "BuildRun") end, { desc = "PreInput Build and Run" })
map("n", "<C-b>", function() Run("execute", "BuildRun") end, { desc = "Build and Run" })
map("n", "<F5>", function() Run("execute", "Run") end, { desc = "Run" })




map("n", "j", "gj", { desc="Go to next visible line" })
map("n", "k", "gk", { desc="Go to prev visible line" })
map("n", "gj", "j", { desc="Go to next line" })
map("n", "gk", "k", { desc="Go to prev line" })
