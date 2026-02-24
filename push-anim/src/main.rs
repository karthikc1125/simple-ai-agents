use std::io::{self, Write};
use std::thread;
use std::time::Duration;

const FRAMES_DATA: &str = include_str!("../frames.txt");

fn main() {
    let frames: Vec<&str> = FRAMES_DATA.split("---FRAME---\n").collect();
    if frames.is_empty() {
        eprintln!("No frames found in data");
        return;
    }

    let mut i = 0;
    // Hide cursor
    print!("\x1b[?25l");
    io::stdout().flush().unwrap();

    loop {
        // Move to top-left (without clearing entire screen to reduce flickering)
        print!("\x1b[H"); 
        println!("{}", frames[i]);
        io::stdout().flush().unwrap();
        
        i = (i + 1) % frames.len();
        
        // Adjust delay based on GIF speed (typically ~100ms)
        thread::sleep(Duration::from_millis(100));
    }
}

// Ensure cursor is shown when process is killed
// Actually we can't easily catch SIGKILL but we can suggest the user to run 'reset' or just handle common ones.
// For now, let's just use a simple loop.
