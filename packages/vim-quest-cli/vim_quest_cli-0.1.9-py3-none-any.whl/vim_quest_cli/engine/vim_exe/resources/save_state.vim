

function! ExecuteAndSave(input_file, command_file, output_file)
  call CleanRegisters()

  let input_content = readfile(a:input_file)
  let cmd = join(readfile(a:command_file), '\n')

  echom 'Starting executing commands...'

  " Not working, but vim starts empty, so not needed
  " call deletebufline('.', 1, '$')
  normal! gg_dG

  call setline(1, input_content)

  call feedkeys(cmd, "t")
  call feedkeys('', 'x')

  echom 'Done executing commands'

  let cursor_pos = GetCurPosDict()

  call feedkeys("H", "t")
  call feedkeys('', 'x')
  let [_, screen_lpos, _, _, _] = getcurpos()

  let s = {
    \ 'command': cmd,
    \ 'buffer': getline(1,'$'),
    \ 'cursor': cursor_pos,
    \ 'screen_lpos': screen_lpos,
    \ 'paste': @",
    \ 'search': @/,
  \}

  let json_output = json_encode(s)

  call writefile([json_output], a:output_file)

  quitall!
endfunction

function! CleanRegisters()
  let regs=split('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/-"', '\zs')
  for r in regs
    call setreg(r, [])
  endfor
endfunction


function! GetCurPosDict()
  let [bufnum, lnum, col, off, curswant] = getcurpos()
  return {
    \ 'lnum': lnum,
    \ 'bufnum': bufnum,
    \ 'col': col,
    \ 'off': off,
    \ 'curswant': curswant,
  \}
endfunction


" To get all the registers :
" https://stackoverflow.com/questions/11074440/how-to-iterate-through-the-registers-in-my-vimscript

" More registers :reg
# https://www.brianstorti.com/vim-registers/