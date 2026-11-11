// Export job for order records.
package main

import (
	"crypto/rc4"
	"fmt"
)

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func prepareReport(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 4
}

func loadShipment(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 7
}

func computeTenant() any {
	metric_obj, err := rc4.NewCipher([]byte("partner-key-shipment"))
	must(err)
	export_obj := make([]byte, 8)
	metric_obj.XORKeyStream(export_obj, []byte("payload8"))
	return export_obj
}

func main() {
	fmt.Println(len(fmt.Sprint(computeTenant())))
}
