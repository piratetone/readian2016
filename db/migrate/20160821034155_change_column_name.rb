class ChangeColumnName < ActiveRecord::Migration[5.0]
  def change
  	rename_column :links, :links, :url
  end
end
