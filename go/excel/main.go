package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"regexp"
	"strings"

	"github.com/tealeg/xlsx"
)

/*

Build for windows:

$ GOOS=windows go build -o transform.exe

*/

var (
	HTML = regexp.MustCompile("<[^>]*?>")
)

func main() {
	inputdir := flag.String("input-dir", "D:/input", "path of the directory")
	outputdir := flag.String("output-dir", "D:/output", "path of the output directory")
	flag.Parse()

	fmt.Println(*inputdir, *outputdir)

	files, err := ioutil.ReadDir(*inputdir)
	if err != nil {
		log.Fatal(err)
	}

	for _, f := range files {
		name := f.Name()
		if !strings.HasSuffix(f.Name(), ".xlsx") {
			fmt.Println(f.Name(), ": skip")
			continue
		}

		fullpath := *inputdir + "/" + name
		infile, err := xlsx.OpenFile(fullpath)
		if err != nil {
			fmt.Println(f.Name(), ": read err", err)
			continue
		}

		outfile := xlsx.NewFile()
		for _, sheet := range infile.Sheets {
			nSheet, err := outfile.AddSheet(sheet.Name)
			if err != nil {
				fmt.Println(f.Name(), ": save err ", err)
				panic(nil)
			}
			sheet.ForEachRow(func(row *xlsx.Row) error {
				nRow := nSheet.AddRow()
				nRow.SetHeight(15) // 按需指定高度

				row.ForEachCell(func(col *xlsx.Cell) error {
					val := HTML.ReplaceAll([]byte(col.String()), nil)
					tmp := strings.ReplaceAll(string(val), "&nbsp;", "")
					tmp = strings.ReplaceAll(tmp, "&lt;", "<")
					tmp = strings.ReplaceAll(tmp, "&gt;", ">")
					val = HTML.ReplaceAll([]byte(tmp), nil)

					nCell := nRow.AddCell()
					nCell.SetString(string(val))

					return nil
				})

				return nil
			})
		}

		err = outfile.Save(*outputdir + "/" + f.Name())
		if err != nil {
			fmt.Println(f.Name(), ": save err ", err)
			continue
		}

		fmt.Println(f.Name(), ": success")
	}
}
