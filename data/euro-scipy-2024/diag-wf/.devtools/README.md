### Creating matrix databes

To create the database with matrices 

```console
python create_database.py
```

### Compiling diagonlization binary

For producing the binary for running the rust project do

```console
cd diager-rs
cargo build --release # compile release version
cp target/release/diager-rs ../../diagar-rs/default # overwrite default binary
```
