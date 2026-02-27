(* OCaml Profiler Validator for EiJack Lab *)

type sample = { name : string; count : int }

let parse_line line =
  match String.split_on_char ',' line with
  | [name; count] -> Some { name; count = int_of_string count }
  | _ -> None

let read_samples filename =
  let ic = open_in filename in
  let rec loop acc =
    try
      match parse_line (input_line ic) with
      | Some s -> loop (s :: acc)
      | None -> loop acc
    with End_of_file ->
      close_in ic;
      acc
  in
  loop []

let validate_performance samples threshold =
  let total_samples = List.fold_left (fun acc s -> acc + s.count) 0 samples in
  List.iter (fun s ->
    let share = (float_of_int s.count /. float_of_int total_samples) *. 100.0 in
    if share > threshold then
      Printf.printf "❌ ALERT: %s is consuming %.2f%% of CPU!\n" s.name share
    else
      Printf.printf "✅ PASS: %s is within limits (%.2f%%)\n" s.name share
  ) samples

let () =
  let samples = read_samples "profiler_data.txt" in
  print_endline "--- 🧪 OCaml Performance Validation ---";
  validate_performance samples 50.0 (* Fail if any function > 50% *)
