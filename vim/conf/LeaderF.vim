scriptencoding utf-8

let g:Lf_ShortcutF = '<C-p>p'
noremap <C-p>P :LeaderfFile .<CR>
noremap <C-p>m :LeaderfMru<CR>
noremap <C-p>f :LeaderfFunction<CR>
noremap <C-p>b :LeaderfBuffer<CR>
noremap <C-p>a :LeaderfTag<CR>

vnoremap <silent> <C-p>gf :<C-U><C-R>=printf("Leaderf rg -F -e %s", leaderf#Rg#visual())<CR><CR>
noremap <silent> <C-p>gf :<C-U><C-R>=printf("Leaderf rg -F -e %s", expand('<cword>'))<CR><CR>

let g:Lf_CommandMap = {
        \ '<C-K>': ['<Up>'],
        \ '<C-J>': ['<Down>'],
        \ '<Up>': ['<C-K>'],
        \ '<Down>': ['<C-J>']
        \ }

" let g:Lf_StlSeparator = {'left': '', 'right': '', 'font': ''}
let g:Lf_StlSeparator = { 'left': '', 'right': '' }

let g:Lf_RootMarkers = ['.project', '.root', '.svn', '.git']
let g:Lf_WorkingDirectoryMode = 'Ac'
let g:Lf_WindowHeight = 0.20
let g:Lf_CacheDirectory = expand('~/.vim/cache')
let g:Lf_ShowRelativePath = 0
let g:Lf_HideHelp = 1
" let g:Lf_StlColorscheme = 'powerline'
let g:Lf_PreviewResult = {'Function': 0, 'BufTag': 0}

" let g:Lf_WindowPosition = 'popup'
let g:Lf_PreviewInPopup = 1 " <C-p> to preview

let g:Lf_CtagsFuncOpts = {
        \ 'rust': '--rust-kinds=f',
        \ }
