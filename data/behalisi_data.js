const marketData = {
  arusha: {
    crops: {
      maize: {
        marketPrice: 148000,
        lastWeek: 138000,
        productionCost: 92000,
        weekly: [144000, 146000, 147500, 149000, 148000],
        monthly: [132000, 136000, 141000, 146000, 148000],
        yearly: [98000, 110000, 120000, 136000, 148000]
      },
      beans: {
        marketPrice: 175000,
        lastWeek: 170000,
        productionCost: 98000,
        weekly: [168000, 171000, 174500, 176000, 175000],
        monthly: [154000, 160000, 166000, 172000, 175000],
        yearly: [120000, 132000, 145000, 164000, 175000]
      },
      rice: {
        marketPrice: 210000,
        lastWeek: 205000,
        productionCost: 120000,
        weekly: [198000, 202000, 206000, 209000, 210000],
        monthly: [182000, 188000, 193000, 201000, 210000],
        yearly: [150000, 165000, 180000, 195000, 210000]
      },
      cassava: {
        marketPrice: 120000,
        lastWeek: 126000,
        productionCost: 76000,
        weekly: [128000, 129000, 124000, 121000, 120000],
        monthly: [136000, 132000, 128000, 123000, 120000],
        yearly: [98000, 103000, 109000, 114000, 120000]
      },
      millet: {
        marketPrice: 136000,
        lastWeek: 128000,
        productionCost: 85000,
        weekly: [127000, 129000, 132000, 135000, 136000],
        monthly: [120000, 122500, 128000, 133000, 136000],
        yearly: [98000, 106000, 119000, 128000, 136000]
      }
    }
  },
  mbeya: {
    crops: {
      maize: {
        marketPrice: 155000,
        lastWeek: 146000,
        productionCost: 96000,
        weekly: [148000, 150500, 152000, 154000, 155000],
        monthly: [135000, 140000, 145000, 151000, 155000],
        yearly: [105000, 118000, 131000, 142000, 155000]
      },
      beans: {
        marketPrice: 184000,
        lastWeek: 180000,
        productionCost: 102000,
        weekly: [176000, 181000, 183500, 185000, 184000],
        monthly: [165000, 171000, 177000, 181000, 184000],
        yearly: [124000, 138000, 155000, 170000, 184000]
      },
      rice: {
        marketPrice: 225000,
        lastWeek: 220000,
        productionCost: 131000,
        weekly: [212000, 216000, 219000, 223000, 225000],
        monthly: [195000, 200000, 208000, 216000, 225000],
        yearly: [155000, 172000, 188000, 206000, 225000]
      },
      cassava: {
        marketPrice: 128000,
        lastWeek: 132000,
        productionCost: 81000,
        weekly: [134000, 133000, 131000, 129000, 128000],
        monthly: [138000, 136000, 133000, 130000, 128000],
        yearly: [102000, 109000, 118000, 123000, 128000]
      },
      millet: {
        marketPrice: 142000,
        lastWeek: 135000,
        productionCost: 90000,
        weekly: [131000, 136000, 139000, 141000, 142000],
        monthly: [124000, 127000, 132000, 137000, 142000],
        yearly: [99000, 108000, 122000, 132000, 142000]
      }
    }
  },
  'dar-es-salaam': {
    crops: {
      maize: {
        marketPrice: 160000,
        lastWeek: 149000,
        productionCost: 97000,
        weekly: [150000, 154000, 157000, 159000, 160000],
        monthly: [137000, 142000, 149000, 156000, 160000],
        yearly: [108000, 121000, 136000, 148000, 160000]
      },
      beans: {
        marketPrice: 190000,
        lastWeek: 184000,
        productionCost: 109000,
        weekly: [180000, 183000, 186500, 188000, 190000],
        monthly: [168000, 174000, 179000, 185000, 190000],
        yearly: [128000, 140000, 155000, 173000, 190000]
      },
      rice: {
        marketPrice: 232000,
        lastWeek: 227000,
        productionCost: 135000,
        weekly: [220000, 224000, 228500, 231000, 232000],
        monthly: [201000, 207000, 214000, 222000, 232000],
        yearly: [160000, 175000, 192000, 210000, 232000]
      },
      cassava: {
        marketPrice: 132000,
        lastWeek: 138000,
        productionCost: 84000,
        weekly: [140000, 139000, 136000, 134000, 132000],
        monthly: [145000, 142000, 138000, 134000, 132000],
        yearly: [106000, 114000, 121000, 127000, 132000]
      },
      millet: {
        marketPrice: 146000,
        lastWeek: 139000,
        productionCost: 91000,
        weekly: [136000, 139000, 142000, 144000, 146000],
        monthly: [128000, 131000, 136000, 140000, 146000],
        yearly: [100000, 112000, 125000, 136000, 146000]
      }
    }
  }
};

const cropLabels = {
  maize: 'Mahindi',
  beans: 'Maharagwe',
  rice: 'Wali',
  cassava: 'Muhogo',
  millet: 'Ulezi'
};

const regionLabels = {
  arusha: 'Arusha',
  mbeya: 'Mbeya',
  'dar-es-salaam': 'Dar es Salaam'
};

const timeFrameLabels = {
  weekly: 'Juma',
  monthly: 'Mwezi',
  yearly: 'Mwaka'
};

window.marketData = marketData;
window.cropLabels = cropLabels;
window.regionLabels = regionLabels;
window.timeFrameLabels = timeFrameLabels;
