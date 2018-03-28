
__script__ = [args] {
  # read excel file
  frame = read_excel(args.filename)

  data = {
    "date" : frame.date,
    "price" : frame.price,
  }

  #
  data
}
