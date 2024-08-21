extern crate npy;

use nalgebra::DMatrix;
use std::f64;

use std::io::Read;
use npy::NpyData;

use std::env;

fn help() {
    println!("
Reads a .npy file reshapes it to a square matrix and computes the absolute eigenvalues.

Usage:

    ./diager <NPY_FILENAME>");
}

fn read_npy(filename: String) -> DMatrix<f64>{
    let mut buf = vec![];
    std::fs::File::open(filename).unwrap()
        .read_to_end(&mut buf).unwrap();

    let data: Vec<f64> = NpyData::from_bytes(&buf).unwrap().to_vec();
    let cols = (data.len() as f64).sqrt() as usize;
    let rows = cols;
    let b = DMatrix::from_row_slice(rows, cols, &data[..]);
    b
}

fn main() {
    let args: Vec<String> = env::args().collect();

    match args.len() {
        2 => {
            let filename_arg = &args[1];
            let filename: String = match filename_arg.parse::<String>() {
                Ok(f) => {
                    f.to_string()
                },
                Err(_) => {
                    eprintln!("error: second argument not an string");
                    help();
                    return;
                },
            };
            let mat = read_npy(filename);
            println!("Matb {}", mat);
            let schur = mat.schur();
            let eigvals = schur.complex_eigenvalues();
            println!("Eigvals {}", eigvals);
        },
        // all the other cases
        _ => {
            // show a help message
            help();
        }
    }
}
