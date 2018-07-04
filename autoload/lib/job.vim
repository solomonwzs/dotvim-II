function! s:Output_Msg_OnError(channel, msg)
    echohl ErrorMsg
    echo 'ERROR: '.a:msg
    echohl None
endfunc


function! s:Job_Node(cmd, next)
    let a:node = {'cmd': a:cmd, 'next': a:next}
    function a:node.jrun(channel, msg)
        echo a:msg
        call job_start(self.cmd, {
                    \ 'callback': self.next.jrun,
                    \ 'err_cb': function('s:Output_Msg_OnError'),
                    \ })
    endfunc
    return a:node
endfunc


function! lib#job#aexec(commands, finish)
    if has('channel') && has('job')
        let a:i = len(a:commands) - 1
        let a:next = {'jrun': a:finish}
        while a:i >= 0
            let a:node = s:Job_Node(a:commands[a:i], a:next)
            let a:next = a:node
            let a:i -= 1
        endwhile
        return a:node
    else
        return
    endif
endfunc
